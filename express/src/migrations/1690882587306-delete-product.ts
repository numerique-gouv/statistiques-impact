import { MigrationInterface, QueryRunner } from 'typeorm';

export class DeleteProduct1690882587306 implements MigrationInterface {
    name = 'DeleteProduct1690882587306';

    public async up(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(`DELETE FROM "indicator"`);
        await queryRunner.query(
            `ALTER TABLE "indicator" DROP CONSTRAINT "FK_aa15d700b2d58418a05c65c071f"`,
        );
        await queryRunner.query(`ALTER TABLE "indicator" DROP COLUMN "productId"`);
        await queryRunner.query(
            `ALTER TABLE "indicator" ADD "nom_service_public_numerique" character varying NOT NULL`,
        );
    }

    public async down(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(`DELETE FROM "indicator"`);
        await queryRunner.query(
            `ALTER TABLE "indicator" DROP COLUMN "nom_service_public_numerique"`,
        );
        await queryRunner.query(`ALTER TABLE "indicator" ADD "productId" uuid`);
        await queryRunner.query(
            `ALTER TABLE "indicator" ADD CONSTRAINT "FK_aa15d700b2d58418a05c65c071f" FOREIGN KEY ("productId") REFERENCES "product"("id") ON DELETE CASCADE ON UPDATE NO ACTION`,
        );
    }
}
