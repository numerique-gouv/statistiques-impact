import { MigrationInterface, QueryRunner } from "typeorm";

export class SwitchBackToProductRelationship1691142565425 implements MigrationInterface {
    name = 'SwitchBackToProductRelationship1691142565425'

    public async up(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(`ALTER TABLE "indicator" RENAME COLUMN "nom_service_public_numerique" TO "productId"`);
        await queryRunner.query(`CREATE TABLE "product" ("id" uuid NOT NULL DEFAULT uuid_generate_v4(), "nom_service_public_numerique" character varying NOT NULL, "metabaseVersion" character varying, CONSTRAINT "UQ_0736f183f1bbb0859e27a381dc8" UNIQUE ("nom_service_public_numerique"), CONSTRAINT "PK_bebc9158e480b949565b4dc7a82" PRIMARY KEY ("id"))`);
        await queryRunner.query(`ALTER TABLE "indicator" DROP COLUMN "productId"`);
        await queryRunner.query(`ALTER TABLE "indicator" ADD "productId" uuid`);
        await queryRunner.query(`ALTER TABLE "indicator" ADD CONSTRAINT "One unique value for indicator by frequence and date" UNIQUE ("productId", "indicateur", "frequence_calcul", "date")`);
        await queryRunner.query(`ALTER TABLE "indicator" ADD CONSTRAINT "FK_aa15d700b2d58418a05c65c071f" FOREIGN KEY ("productId") REFERENCES "product"("id") ON DELETE CASCADE ON UPDATE NO ACTION`);
    }

    public async down(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(`ALTER TABLE "indicator" DROP CONSTRAINT "FK_aa15d700b2d58418a05c65c071f"`);
        await queryRunner.query(`ALTER TABLE "indicator" DROP CONSTRAINT "One unique value for indicator by frequence and date"`);
        await queryRunner.query(`ALTER TABLE "indicator" DROP COLUMN "productId"`);
        await queryRunner.query(`ALTER TABLE "indicator" ADD "productId" character varying NOT NULL`);
        await queryRunner.query(`DROP TABLE "product"`);
        await queryRunner.query(`ALTER TABLE "indicator" RENAME COLUMN "productId" TO "nom_service_public_numerique"`);
    }

}
